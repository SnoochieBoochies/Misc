set nocompatible
execute pathogen#infect()

 filetype indent plugin on
 syntax on
 syntax enable
 colorscheme monokai
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
""autocmd VimEnter * NERDTree
""autocmd VimEnter * wincmd p
""open files in new tabs
""autocmd VimEnter * tab all
""autocmd BufAdd * exe 'tablast | tabe "' . expand( "<afile") . '"'
map <C-w><right> :tabn<cr>
map <C-w><left> :tabp<cr>
""tabs mapping
""nnoremap <C-S-t> :NERDTreeTabsToggle<cr>
""let g:nerdtree_tabs_open_on_console_startup=1
:nmap p :pu<CR>
" tab navigation like firefox
""nnoremap <C-S-tab> :tabp<cr>
""nnoremap <C-tab>   :tabn<cr>
nnoremap <C-t>     :tabnew<cr>
"inoremap <C-S-tab> <Esc>:tabp<CR>i
"inoremap <C-tab>   <Esc>:tabn<CR>i
"inoremap <C-t>     <Esc>:tabnew<CR>

""Trying out explorer instead of NERDTree
""let g:netrw_liststyle=3
""let mapleader=" "
""map <C-e> :Texplore<cr>
""Toggle Vexplore with Ctrl-e
function! ToggleVExplorer()
  if exists("t:expl_buf_num")
      let expl_win_num = bufwinnr(t:expl_buf_num)
      if expl_win_num != -1
          let cur_win_nr = winnr()
          exec expl_win_num . 'wincmd w'
          close
          exec cur_win_nr . 'wincmd w'
          unlet t:expl_buf_num
      else
          unlet t:expl_buf_num
      endif
  else
      exec '1wincmd w'
      Vexplore
      let t:expl_buf_num = bufnr("%")
  endif
endfunction
map <silent> <C-e> :call ToggleVExplorer()<CR>

" Hit enter in the file browser to open the selected
" file with :vsplit to the right of the browser.
let g:netrw_browse_split = 4
let g:netrw_altv = 1
" absolute width of netrw window
let g:netrw_winsize = -28
" tree-view
let g:netrw_liststyle = 4

" Change directory to the current buffer when opening files.
set autochdir
