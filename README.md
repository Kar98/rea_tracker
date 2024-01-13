# Real estate tracker
$env:PYTHONPATH="D:\Coding\real_estate_tracker"
cd D:
cd D:\Coding\real_estate_tracker
python web_scraper\web_scraper.py
python app\run.py
Write-Host "Press any key to continue ....."
$x = $host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")