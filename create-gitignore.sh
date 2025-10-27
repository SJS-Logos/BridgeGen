OUTPUT=".gitignore"

curl -s "https://raw.githubusercontent.com/github/gitignore/main/C++.gitignore" >"$OUTPUT"
curl -s "https://raw.githubusercontent.com/github/gitignore/main/C.gitignore" >>"$OUTPUT"
curl -s "https://raw.githubusercontent.com/github/gitignore/main/VisualStudio.gitignore" >>"$OUTPUT"

cat >> "$OUTPUT" <<'EOF'

# Ignore contents created by cmake in the [B]uild/ folder
[Bb]uild/

