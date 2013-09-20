# .bashrc

# Source global definitions
if [ -f /etc/bashrc ]; then
	. /etc/bashrc
fi

# User specific aliases and functions
alias vi='vim'
function EXT_COLOR () { 
  echo -ne "\e[38;5;$1m"; 
}
function CLOSE_COLOR () {
    echo -ne '\e[m';
}
export LS_COLORS='di=38;5;108:fi=00:*svn-commit.tmp=31:ln=38;5;116:ex=38;5;186'
#export PS1='`EXT_COLOR 187`\u@\h`EXT_COLOR 174` \W \$\[\033[00m\] > '
export PS1="\[`EXT_COLOR 187`\]\u@\h\[`CLOSE_COLOR`\]\[`EXT_COLOR 174`\] \W \$ \[`CLOSE_COLOR`\] > "

export FUSIONWORKS_HOME=/media/backup/eclipse-workspace/testHome/home
export FUSIONWORKS_PROD=/media/backup/eclipse-workspace/testHome/prod
export JAVA_HOME=/opt/java/jdk1.7.0_09
export ORACLE_HOME=/opt/oracle/product/11.2.0.3

export PATH=$FUSIONWORKS_PROD/bin:$JAVA_HOME/bin:$ORACLE_HOME/bin:$HOME/bin:/opt/solidDB/solidDB-7.0.0.4-IF007/bin:/usr/lib64/qt-3.3/bin:/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$FUSIONWORKS_PROD/lib
