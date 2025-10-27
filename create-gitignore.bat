SET OUTPUT=".gitignore"

curl -s "https://raw.githubusercontent.com/github/gitignore/main/C++.gitignore" >%OUTPUT%
curl -s "https://raw.githubusercontent.com/github/gitignore/main/VisualStudio.gitignore" >>%OUTPUT%
curl -s "https://raw.githubusercontent.com/github/gitignore/main/Global/JetBrains.gitignore" >>%OUTPUT%

ECHO. >>%OUTPUT%
ECHO # Ignore contents created by cmake in the [B]uild/ folder >>%OUTPUT%
ECHO [Bb]uild/ >>%OUTPUT%

