# Draft Book 1 print PDF

The interior PDF is served at `/reviewbook/book1-interior.pdf` and viewed at `/reviewbook`.

It is **not** committed to git (too large). Upload after regenerating:

```powershell
npm run export:print-pdfs
aws s3 cp exports/scribus/book1/pdf/book1-interior.pdf `
  s3://learn-bosnian-frontend-prod/reviewbook/book1-interior.pdf `
  --content-type application/pdf
aws cloudfront create-invalidation --distribution-id E22QTEONDMDA3Z --paths "/reviewbook/*"
```

Local preview: copy the PDF into this folder as `book1-interior.pdf`, then `npm start` in `frontend/`.
