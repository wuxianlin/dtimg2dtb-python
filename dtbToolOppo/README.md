# dtbtool
Pack dtb files to dt image

usage:
---------
     dtbTool [options] -o <output file> <input DTB path>
       options:
       --output-file/-o     output file
       --dtc-path/-p        path to dtc
       --page-size/-s       page size in bytes
       --dt-tag/-d          alternate QCDT_DT_TAG
       --verbose/-v         verbose
       --force-v2/-2        use dtb v2 format
       --force-v3/-3        use dtb v3 format
       --help/-h            this help screen

example:
---------
     ./dtbToolOppo -3 -o dtb.img -s 2048 -p dtc/ dtb/

Source:
---------
[dtbTool](https://www.codeaurora.org/cgit/quic/la/device/qcom/common/)<br /> 
[dtbToolOppo](https://github.com/CyanogenMod/android_device_oppo_msm8939-common)<br /> 
