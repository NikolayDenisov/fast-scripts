set background=dark

"Настроим кол-во символов пробелов, которые будут заменять \t
set tabstop=4
set shiftwidth=4
set smarttab
"включим автозамену по умолчанию
set et 

"Попросим Vim переносить длинные строки
set wrap

"Включим автоотступы для новых строк
set ai

"Включим отступы в стиле Си
set cin

"Показываем табы в начале строки точками
set listchars=tab:··
set list

" Использовать цветовую схему ron для выделения текста
colorscheme ron

"Переносить целые слова
set linebreak

"включает поддержку мыши при работе в терминале (без GUI)
set mouse=a
"скрывать мышь в режиме ввода текста
set mousehide 

"показывать первую парную скобку после ввода второй
set showmatch 

"использовать больше цветов в терминале
set t_Co=256 

"использовать диалоги вместо сообщений об ошибках
set confirm

"Автоматически перечитывать конфигурацию VIM после сохранения
autocmd! bufwritepost $MYVIMRC source $MYVIMRC

"Проблема красного на красном при spellchecking-е решается такой строкой в .vimrc
highlight SpellBad ctermfg=Black ctermbg=Red
"при закрытии файла сохранить 'вид'
au BufWinLeave *.* silent mkview
"при открытии - восстановить сохранённый
au BufWinEnter *.* silent loadview
"backspace обрабатывает отступы, концы строк
set backspace=indent,eol,start
"не использовать своп-файл (в него скидываются открытые буферы)
set noswapfile
"вместо писка бипером мигать курсором при ошибках ввода
set visualbell
"необходимо установить для того, чтобы *.h файлам присваивался тип c, а не cpp
let c_syntax_for_h="" 
"Умные отступы (например, автоотступ после {)

set smartindent 
"Enable line numbers
set number
"Highlight current line
set cursorline
"Show “invisible” characters
"set lcs=tab:▸\ ,trail:·,eol:¬,nbsp:_
"Show the current mode
set showmode
"Show the filename in the window titlebar
set title
"Show the (partial) command as it’s being typed
set showcm
