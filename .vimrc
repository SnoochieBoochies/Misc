set nocompatible
execute pathogen#infect()

 filetype indent plugin on
 syntax on
 au BufRead,BufNewFile *.dsd set filetype=dsd
 set hidden
 set wildmenu
 set showcmd
 set hlsearch
 set ignorecase
 set smartcase
 set backspace=indent,eol,start
 set autoindent
 set smartindent
 set ruler
 set laststatus=2
 set confirm
 set visualbell
 set mouse=a
 set cmdheight=2
 set number
 set shiftwidth=4
 set tabstop=4
 ""set softtabstop=4
 set expandtab
 set statusline=%t[%{strlen(&fenc)?&fenc:'none'},%{&ff}]%h%m%r%y%=%c,%l/%L\ %P
""set term=ansi
map <Esc>[B <Down>
augroup reload_vimrc " {
  autocmd!
  autocmd BufWritePost $MYVIMRC source $MYVIMRC
augroup END " }

""NERDTree
autocmd VimEnter * NERDTree
""autocmd VimEnter * wincmd p
""open files in new tabs
autocmd VimEnter * tab all
""autocmd BufAdd * exe 'tablast | tabe "' . expand( "<afile") . '"'
map <C-w><right> :tabn<cr>
map <C-w><left> :tabp<cr>
""tabs mapping
nnoremap <C-S-t> :NERDTreeTabsToggle<cr>
let g:nerdtree_tabs_open_on_console_startup=1
:nmap p :pu<CR>
" tab navigation like firefox
"nnoremap <C-S-tab> :tabp<cr>
"nnoremap <C-tab>   :tabn<cr>
"nnoremap <C-t>     :tabnew<cr>
"inoremap <C-S-tab> <Esc>:tabp<CR>i
"inoremap <C-tab>   <Esc>:tabn<CR>i
"inoremap <C-t>     <Esc>:tabnew<CR>


