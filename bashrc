# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
alias vi='vim'
alias squ='~/squirrel-sql-3.5.0/squirrel-sql.sh &'
function EXT_COLOR () { 
  echo -ne "\e[38;5;$1m"; 
}
function CLOSE_COLOR () {
    echo -ne '\e[m';
}
export LS_COLORS='di=38;5;108:fi=00:*svn-commit.tmp=31:ln=38;5;116:ex=38;5;186'
#export PS1='`EXT_COLOR 187`\u@\h`EXT_COLOR 174` \W \$\[\033[00m\] > '
#export PS1="\[`EXT_COLOR 187`\]\u@\h\[`CLOSE_COLOR`\]\[`EXT_COLOR 174`\] \W \$ \[`CLOSE_COLOR`\] > "
export PS1="\n\[`EXT_COLOR 143`\]\w \[`CLOSE_COLOR`\]
\[`EXT_COLOR 187`\]\u@\h\[`CLOSE_COLOR`\]\[`EXT_COLOR 174`\] \$ \[`CLOSE_COLOR`\] > "

export FUSIONWORKS_HOME=/home/snooch/products/FW9.1/home
export FUSIONWORKS_PROD=/home/snooch/products/FW9.1/prod
#export FUSIONWORKS_HOME=/home/snooch/products/TRD/home
#export FUSIONWORKS_PROD=/home/snooch/products/TRD/prod
export FW_CONSOLE_PORT_ON=1
export JAVA_HOME=/usr/java/jdk1.7.0_45
export ANT_HOME=/opt/apache-ant-1.8.1
export M2_HOME=/opt/apache-maven-3.0.5
export ORACLE_HOME=/opt/oracle/product/12.1.0.1/client
export VOLT_HOME=/opt/volt/voltdb-ent-4.6
export VOLTDB_BIN=$VOLT_HOME/bin
#atf performance specific opt
export EXTRACLASSPATH=/home/snooch/workspace/voltComponents_trunk/tests/acceptance/performance/CompositeCommands
export EXTRAPATH=/home/snooch/workspace/voltComponents_trunk/tests/acceptance/performance/scripts
export PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$M2_HOME/bin:$ORACLE_HOME/bin:$HOME/bin:/opt/solidDB/solidDB-7.0.0.4-IF007/bin:$VOLT_HOME/bin:/usr/lib64/qt-3.3/bin:/opt/Sublime\ Text\ 2/:/opt/boost/boost_1_55_0:$EXTRACLASSPATH:$EXTRAPATH:$PATH

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/gmock-1.6.0/lib:/opt/boost/boost_1_55_0/stage/lib
export GTK2_RC_FILES="/etc/gtk-2.0/gtkrc:$HOME/.gtkrc-2.0"
export work=~/workspace
export testHome=/home/snooch/workspace/voltComponents_trunk/tests/acceptance
#export DISPLAY=localhost:0.0
export BROWSER="chromium"
#enable cores 
ulimit -c unlimited


#tmux history of bash
export HISTCONTROL=ignoredups:erasedups

#save+reload after each command
#export PROMPT_COMMAND="history -a; history -c; history -r; $PROMPT_COMMAND"
