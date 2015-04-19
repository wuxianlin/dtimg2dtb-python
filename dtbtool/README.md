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
       --help/-h            this help screen

example:
---------
     ./dtbToolCM -2 -o dtb.img -s 2048 -p dtc/ dtb/

Source:
---------
[dtbTool](https://www.codeaurora.org/cgit/quic/la/device/qcom/common/)<br /> 
[dtbToolCM](https://github.com/CyanogenMod/android_device_qcom_common)<br /> 
