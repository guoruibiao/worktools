# awesome trasnlator for myself.

# idea
translate whatever in my system clipboard

# dependency
`pbpaste`, which can access directly, and the optional command is`pbcopy`.

# usage
thus how to use it?
1. download the scripts
```
wget or git clone or whatever you can download.
```
do not forget the absolute path in your computer, such as `/Users/biao/Code/trans`

2. add `alias` to your `~/.bashrc` or `~/.zshrc`
```
alias starttrans='cd /Users/biao/Code/trans && bash starttrans.sh'
alias stoptrans='cd /Users/biao/Code/trans && bash stoptrans.sh'
```

3. activation those alias
```
source ~/.zshrc
or 
source ~/.bashrc
```

4. enjoy it :)
