import Foundation
import PDFKit
import AppKit

let fileManager = FileManager.default
let currentDir = fileManager.currentDirectoryPath
let docsDir = (currentDir as NSString).appendingPathComponent("documents")
let renderedBaseDir = (docsDir as NSString).appendingPathComponent("rendered")

try? fileManager.createDirectory(atPath: renderedBaseDir, withIntermediateDirectories: true, attributes: nil)

var enumerator = fileManager.enumerator(atPath: docsDir)
var pdfPaths: [String] = []

while let file = enumerator?.nextObject() as? String {
    if file.hasPrefix("rendered") { continue }
    if file.lowercased().hasSuffix(".pdf") {
        pdfPaths.append(file)
    }
}

pdfPaths.sort()

print("Found \(pdfPaths.count) PDFs in documents/")

var manifest: [String: [String: Any]] = [:]

for relPdfPath in pdfPaths {
    let fullPdfPath = (docsDir as NSString).appendingPathComponent(relPdfPath)
    guard let pdfDoc = PDFDocument(url: URL(fileURLWithPath: fullPdfPath)) else {
        print("Failed to open PDF: \(relPdfPath)")
        continue
    }
    
    let pageCount = pdfDoc.pageCount
    let pdfNameWithoutExt = ((relPdfPath as NSString).lastPathComponent as NSString).deletingPathExtension
    let relDir = (relPdfPath as NSString).deletingLastPathComponent
    
    let targetSubDir = (renderedBaseDir as NSString).appendingPathComponent(relDir).appending("/\(pdfNameWithoutExt)")
    try? fileManager.createDirectory(atPath: targetSubDir, withIntermediateDirectories: true, attributes: nil)
    
    var renderedPages: [String] = []
    
    for pageIdx in 0..<pageCount {
        let pageNum = pageIdx + 1
        let outFileName = "page-\(pageNum).png"
        let outFullPath = (targetSubDir as NSString).appendingPathComponent(outFileName)
        let outRelPath = "documents/rendered/\(relDir.isEmpty ? "" : relDir + "/")\(pdfNameWithoutExt)/\(outFileName)"
            .replacingOccurrences(of: "//", with: "/")
        
        renderedPages.append(outRelPath)
        
        // Check if file already exists and is newer than PDF
        if fileManager.fileExists(atPath: outFullPath) {
            if let pdfAttr = try? fileManager.attributesOfItem(atPath: fullPdfPath),
               let imgAttr = try? fileManager.attributesOfItem(atPath: outFullPath),
               let pdfMod = pdfAttr[.modificationDate] as? Date,
               let imgMod = imgAttr[.modificationDate] as? Date,
               imgMod >= pdfMod {
                // Up to date, skip rendering
                continue
            }
        }
        
        guard let page = pdfDoc.page(at: pageIdx) else { continue }
        let bounds = page.bounds(for: .mediaBox)
        let scale: CGFloat = 2.0 // 2x Retina resolution (~150-200 DPI)
        let targetSize = NSSize(width: bounds.width * scale, height: bounds.height * scale)
        
        let image = NSImage(size: targetSize)
        image.lockFocus()
        
        guard let context = NSGraphicsContext.current?.cgContext else {
            image.unlockFocus()
            continue
        }
        
        // Fill white background (crucial for transparent PDF backgrounds)
        context.setFillColor(CGColor(red: 1.0, green: 1.0, blue: 1.0, alpha: 1.0))
        context.fill(CGRect(origin: .zero, size: targetSize))
        
        context.saveGState()
        context.scaleBy(x: scale, y: scale)
        
        // Render PDF page
        page.draw(with: .mediaBox, to: context)
        
        context.restoreGState()
        image.unlockFocus()
        
        // Save as PNG
        if let tiffData = image.tiffRepresentation,
           let bitmapRep = NSBitmapImageRep(data: tiffData),
           let pngData = bitmapRep.representation(using: .png, properties: [:]) {
            try? pngData.write(to: URL(fileURLWithPath: outFullPath))
        }
    }
    
    let docKey = "documents/\(relPdfPath)"
    manifest[docKey] = [
        "pageCount": pageCount,
        "pages": renderedPages
    ]
    print("[\(pageCount) pages] Rendered: \(relPdfPath)")
}

let manifestPath = (docsDir as NSString).appendingPathComponent("rendered_manifest.json")
if let jsonData = try? JSONSerialization.data(withJSONObject: manifest, options: [.prettyPrinted, .sortedKeys]) {
    try? jsonData.write(to: URL(fileURLWithPath: manifestPath))
    print("Wrote rendered_manifest.json with \(manifest.count) documents.")
}
