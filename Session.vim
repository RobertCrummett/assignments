" Since the directory tree is not very deep,
" but it is annoying to manually specify
" the directory each time, I let the path
" search recursively.
set path+=**
" Now we use the `.gitignore` file to hide
" file types from the wildmenu that are
" not relevant --- that is, everything 
" besides `.tex` files
set wildignore+=**/*.log,**/*.pdf,**/.git/*
