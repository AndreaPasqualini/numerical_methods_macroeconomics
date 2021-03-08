Get-ChildItem -File | Where-Object {$_.Extension -eq ".tex"} | ForEach-Object { latexmk.exe -pdf $_.FullName }

# Remove everything except files with extensions {tex, sty, pdf, bib, md, ps1}
Get-ChildItem -File | `
  Where-Object { $_.Extension -ne ".tex" -and $_.Extension -ne ".sty" -and $_.Extension -ne ".pdf" -and $_.Extension -ne ".bib" -and $_.Extension -ne ".md" -and $_.Extension -ne ".ps1" } | `
  Remove-Item
  