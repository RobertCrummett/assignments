set path+=**
let &wildignore=join(map(split(substitute(substitute(
            \ netrw_gitignore#Hide(), '\.\*', '*', 'g'), '\\.', '.', 'g'), ','),
            \ "v:val.','.v:val.'/'"), ',')
let g:netrw_list_hide=netrw_gitignore#Hide() .. '.*\.swp$'
