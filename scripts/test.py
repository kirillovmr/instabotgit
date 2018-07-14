import git, os, shutil

DIR_NAME = "temp"
REMOTE_URL = "https://github.com/kirillovmr/instabotgit.git"

g = git.cmd.Git(DIR_NAME)
g.pull()
