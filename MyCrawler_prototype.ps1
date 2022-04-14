
function Invoke-MecabPython ($s) {
    $pythonPath = "{0}\python\mecab_analyze.py" -f $PSScriptRoot
    Invoke-Expression -Command ("python -B '{0}' '{1}'" -f $pythonPath, $s)
}

function Start-Parse {
	param ($responsestr)
	Write-Host "[Start-Parse] START"

	$findkey_http = 'https://'
    $endofurl = '&amp;'
	$readpoint = 0
	$urlarr = @()
	$searchstr = $responsestr

	# mecab sample
	Invoke-MecabPython($searchkeyfile)

	do{
		$searchstrlen = $searchstr.length
		Write-Host "searchstr length : $searchstrlen"
		$starturl = $searchstr.IndexOf($findkey_http)
		Write-Host "starturl : $starturl"
		if ($starturl -eq "-1") {
			break
		}
		$endurl = $searchstr.IndexOf($endofurl)
		Write-Host "endurl : $endurl"

		while ($starturl -gt $endurl -and ($searchstr.IndexOf($endofurl) -ne -1)) {
			$starturl = $searchstr.IndexOf($findkey_http)
			Write-Host "starturl : $starturl"
			$endurl = $searchstr.IndexOf($endofurl)
			Write-Host "endurl : $endurl"
			$readpoint = $starturl - 1
			$searchstr_tmp = $searchstr.Substring($readpoint, ($searchstrlen - $readpoint))
			Write-Host "searchstr tmp length : "$searchstr_tmp.length
			$searchstr = $searchstr_tmp
			$searchstrlen = $searchstr.length
		}
		$urlstr = $searchstr[$starturl .. ($endurl -1)] -join '' # 文字列からURLを切り出す

		if($urlstr -match $findkey_http){
			$url = [System.Web.HttpUtility]::UrlDecode($urlstr) # URLをデコードする
		}else{
			continue
		}
		Write-Host "url found : $url"
		$urlarr += $url
		$readpoint = $endurl
		$searchstr_tmp = $searchstr.Substring($readpoint, ($searchstrlen - $readpoint))
		$searchstr = $searchstr_tmp
	}while($searchstr.IndexOf($endofurl) -ne -1)

	if($urlarr.Count -eq 0){
		Write-Host "There is no url!"
	}else{
		$urlcnt = $urlarr.Count
		Write-Host "There are $urlcnt urls found!"
		Write-Host $urlarr
		$urlarr | Add-Content $logfile -Encoding UTF8
	}
	Write-Host "[Start-Parse] END"

	return
}

function Get-Word {
	param ($arr)
	Write-Host "[Get-Word] START"
	$count = $arr.Count

	if($count -ge 2){
		$wordnum = Get-Random -Maximum $count -Minimum 0
	}elseif ($count -eq 1) {
		$wordnum = 0
	}else {
		Write-Host "There is no data!"
		return $null
	}
	$word = $arr[$wordnum]
	Write-Host "word: $word"
	Write-Host "[Get-Word] END"
	return $word
}
function Start-Crawling {
	param ()
	Write-Host "[Start-Crawling] START"

	$uri = "https://www.google.com/search?sourceid=chrome&ie=UTF-8"
	$searchkey = Get-Word($searchkeyarr)
	$uri += ('&' + 'q=' + $searchkey)
	Write-Host "$uri"
	"URI: $uri" | Add-Content $logfile -Encoding UTF8

	$response = Invoke-WebRequest -Uri $uri -UseBasicParsing
	$responsestr = [string]$response
	# parse response and list urls
	Start-Parse($responsestr)

#	$response | Add-Content $logfile -Encoding UTF8
#	$response.Content | Add-Content $logfile -Encoding UTF8

	Write-Host "[Start-Crawling] END"

}

function Show-File {
	param ($filename)

	Write-Host "[Show-File] START"
	$keys = Get-Content -LiteralPath $filename -Encoding UTF8
	$keyarr = $keys -split ','
	$num = 0
	foreach ($key in $keyarr) {
		$num++
		Write-Host "$num : $key"
	}

	Write-Host "[Show-File] END"
}

# main function
Add-Type -AssemblyName System.Web	# url encode and decode

# global variables
$logfile = "./logfile.log"
$searchkeyfile = "./Searchkey.csv"
$candidatefile = "./Candidate.csv"
$partition = "==========================="
$comma = ','

$searchkeys = Get-Content -LiteralPath $searchkeyfile -Encoding UTF8
$searchkeyarr = $searchkeys -split ','

while ($true) {
	Write-Host ""
	Write-Host "[[MAIN FUNCTION]]"
	Write-Host "mode is below."
	Write-Host "list candidates : l"
	Write-Host "candidates to be searchkeys : s"
	Write-Host "list search key : k"
	Write-Host "quit : q"
	Write-Host "start crawling : other"

	$partition | Add-Content $logfile -Encoding UTF8

	$select = Read-Host "<<MODE SELECT>>"
	if(($select -eq 'l') -or ($select -eq 'L')){
		# list candidates
		Show-File($candidatefile)
	}elseif (($select -eq 's') -or ($select -eq 'S')) {
		# candidates to be searchkeys
		Show-File($candidatefile)

		while(0){
			Write-Host "Select number you want to be searchkey."
			Write-Host "q: cancel"
			$select = Read-Host "<<SELECT NUMBER>>"
			if($select -eq 'q'){
				break
			}
			$candidates = Get-Content -LiteralPath $candidatefile -Encoding UTF8
			$candidatearr = $candidates -split ','
			$addstr = $comma + $candidatearr[$select]
			$addstr | Add-Content $searchkeyfile -Encoding UTF8
		}

	}elseif (($select -eq 'k') -or ($select -eq 'K')) {
		# list searchkeys
		Show-File($searchkeyfile)
	}elseif (($select -eq 'q') -or ($select -eq 'Q')) {
		# quit
		$date = Get-Date
		Write-Host "terminate this program ($date)"
		Start-Sleep 1
		exit		
	}else {
		# start crawling
		Start-Crawling	
	}   
}
