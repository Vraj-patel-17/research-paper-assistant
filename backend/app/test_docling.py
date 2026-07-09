from app.services.docling_service import DoclingService

print("1. Creating service...")

service = DoclingService()

print("2. Service created.")

print("3. Parsing PDF...")

doc = service.parse_pdf(r"D:\Downloads\Basics of Web Designing.pdf")

markdown = doc.export_to_markdown()

print(markdown[:3000])
print(doc.num_pages)
print(len(doc.tables))
print(len(doc.pictures))