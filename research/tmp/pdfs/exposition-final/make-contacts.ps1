Add-Type -AssemblyName System.Drawing
$imageRoot = Join-Path $PSScriptRoot '.'
$pages = @(Get-ChildItem -LiteralPath $imageRoot -Filter 'page-*.png' | Sort-Object Name)
$font = New-Object System.Drawing.Font('Arial', 12)
$brush = [System.Drawing.Brushes]::Black
$cols = 5
$rows = 4
$cellWidth = 405
$cellHeight = 525
for ($offset = 0; $offset -lt $pages.Count; $offset += $cols*$rows) {
    $sheet = New-Object System.Drawing.Bitmap(($cols*$cellWidth), ($rows*$cellHeight))
    $canvas = [System.Drawing.Graphics]::FromImage($sheet)
    $canvas.Clear([System.Drawing.Color]::FromArgb(230,230,230))
    for ($local = 0; $local -lt $cols*$rows -and $offset+$local -lt $pages.Count; $local++) {
        $pageFile = $pages[$offset+$local]
        $pageImage = [System.Drawing.Image]::FromFile($pageFile.FullName)
        $x = ($local % $cols)*$cellWidth+10
        $y = [math]::Floor($local/$cols)*$cellHeight+25
        $canvas.DrawImage($pageImage, $x, $y, $pageImage.Width, $pageImage.Height)
        $canvas.DrawString($pageFile.BaseName, $font, $brush, $x, $y-22)
        $pageImage.Dispose()
    }
    $canvas.Dispose()
    $index = [math]::Floor($offset/($cols*$rows))+1
    $sheet.Save((Join-Path $imageRoot ('contact-'+$index+'.png')), [System.Drawing.Imaging.ImageFormat]::Png)
    $sheet.Dispose()
}
$font.Dispose()
Write-Output ('Contact sheets made for '+$pages.Count+' pages.')
