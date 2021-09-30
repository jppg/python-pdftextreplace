#pip install pymupdf
import fitz

REQUESTED_DPI = 300
DEFAULT_DPI = 72

filename = 'filename.pdf'
doc = fitz.open(filename)
doc_out = fitz.open() 

replacements = [
    ("text_to_replace", "",)
]

print(doc.metadata)
for page in doc.pages(0, doc.page_count, 1):
    for txt_from, txt_to in replacements:
        # Search for existing text
        area: fitz.Rect = page.search_for(txt_from)[0]
        # Use redact annotation to remove the text
        page.add_redact_annot(area)
        page.apply_redactions()
        # Insert replacement text in its place
        font_size = area.height
        text_point = area.bottom_left
        text_point.y -= font_size / 4  # not sure why 4 is the right value here
        page.insert_text(text_point, txt_to, fontsize=font_size, fontname="courier")
    
# Save document as PDF
doc.save("output_"+filename, garbage=4, deflate=True)
doc.close()