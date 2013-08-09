set nocompatible
execute pathogen#infect()

 filetype indent plugin on
 syntax on
 set hidden
 set wildmenu
 set showcmd
 set hlsearch
 set ignorecase
 set smartcase
 set backspace=indent,eol,start
 set autoindent
 set nostartofline
 set ruler
 set laststatus=2
 set confirm
 set visualbell
 set mouse=a
 set cmdheight=2
 set number
 set shiftwidth=2
 set softtabstop=4
 set expandtab
 set statusline=%t[%{strlen(&fenc)?&fenc:'none'},%{&ff}]%h%m%r%y%=%c,%l/%L\ %P
""set term=ansi
