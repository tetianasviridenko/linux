import os
import pwd
def get_user_info():
    user_name = os.getlogin()
    user_info = pwd.getpwnam(user_name)
    return {
            "User Name": user_name,
            "User ID": user_info.pw_uid,
            "Group ID": user_info.pw_gid,
            "Home Directory": user_info.pw_dir,
            "Shell": user_info.pw_shell
            }
if __name__ == "__main__":
    user_info = get_user_info()
    for key, value in user_info.items():
        print(f"{key}: {value}")
