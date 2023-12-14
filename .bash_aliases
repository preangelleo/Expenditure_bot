alias nb='nano /home/preangel/.bash_aliases'
alias sb='source ~/.bashrc'
alias sba='source ~/.bash_aliases'
alias a='alias'
alias ll='ls -alF'
alias la='ls -A'
alias c='clear'
alias cb='cd /home/preangel/backup'

alias pip='pip3'
alias pm='pm2'

alias pipr='pip3 install -r requirements.txt'

alias pmr='pm2 restart'
alias pmra='pm2 restart all'
alias pms='pm2 stop'
alias pmsall='pm2 stop all'
alias pmdall='pm2 delete all'
alias pml='pm2 list'
alias pmlg='pm2 logs'
alias py='python3'

alias pmwh='pm2 start start_flask.sh'
alias prwh='pm2 restart wh'
alias pmep='pm2 start Telegram_bot.py --name ep --interpreter python3'
alias prep='pm2 restart ep'

alias cflask='chmod +x start_flask.sh'

alias ceai='cd /home/preangel/Expenditure_bot && conda activate expenditure_ai'