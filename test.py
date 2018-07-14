import os
os.chdir("temp")
os.system("git remote add instabotgit https://github.com/kirillovmr/instabotgit")
os.system("git fetch instabotgit master")
os.system("git reset --hard FETCH_HEAD")
os.system("git clean -df")
