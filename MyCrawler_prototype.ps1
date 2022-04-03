
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
    $response = Invoke-WebRequest -Uri $uri -UseBasicParsing

	$response | Add-Content $logfile -Encoding UTF8
	$response.Content | Add-Content $logfile -Encoding UTF8

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
