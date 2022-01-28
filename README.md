# date_repo
repo and submodules aren't dated, allow request to pull a submodule at a date.

## running
This tool can be run from within an initialized repo, or to "init" a repo and pull its dependencies. Full support is not yet available for initializing a repo, but a sample command line for use from within a branch of the android common kernel:
`python3 ~/repos/date_repo/date_repo.py --date 2021-07-06`

## sample output:
```shell
mariomain@raichu-off:~/raichu-storage/repos/common-android11-5.4$ python3 ~/repos/date_repo/date_repo.py --date 2021-07-06
/home/mariomain/repos/date_repo/date_repo.py:66: DeprecationWarning: This method will be removed in future versions.  Use 'list(elem)' or iteration over elem instead.
  for i in default_xml.getchildren():
repo build checking out commit 7d8f18edb79f3d3d85966226e5b23ae57669b6c0 dated 2021-07-01 10:06:57 +0000
repo common checking out commit f8878f4c597b94c91e06592105f6e60febd4125c dated 2021-07-05 12:31:35 +0530
repo common-modules/virtual-device checking out commit e40ae31320073a57c04c40b916f84801c291f06f dated 2021-06-18 22:06:14 +0200
repo hikey-modules checking out commit 33d4b7f884500689a297df156b1c0a29e1c525da dated 2020-08-25 19:57:50 +0800
WARNING: no commit for repo prebuilts/kernel-build-tools before 2021-07-06, earliest 2021-07-23 17:31:18 +0100
WARNING: no commit for repo prebuilts/build-tools before 2021-07-06, earliest 2021-07-29 11:46:04 +0000
WARNING: no commit for repo prebuilts-master/clang/host/linux-x86 before 2021-07-06, earliest 2021-07-26 11:46:32 +0100
repo prebuilts/gcc/linux-x86/aarch64/aarch64-linux-android-4.9 checking out commit 98dce673ad97a9640c5d90bbb1c718e75c21e071 dated 2020-04-10 04:19:19 +0000
repo prebuilts/gcc/linux-x86/arm/arm-linux-androideabi-4.9 checking out commit 3e1d1fd459f5bb401479602c44448764f54ffe57 dated 2020-04-10 04:28:39 +0000
WARNING: no commit for repo prebuilts/gcc/linux-x86/x86/x86_64-linux-android-4.9 before 2021-07-06, earliest 2021-07-26 11:56:07 +0100
repo tools/mkbootimg checking out commit d0d261f3b0f57105f570a9878e748d817a3c5e60 dated 2021-05-05 15:10:50 +0800
```