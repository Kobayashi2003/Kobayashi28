# how to turn off phantom processes killing (Android 12 or later, not root required)

- Android 12L or later

```shell
adb shell "settings put global settings_enable_monitor_phantom_procs false"

# if you want to enable it again
# adb shell "settings put global settings_enable_monitor_phantom_procs true"
```

- Android 12, no GMS
  
```shell
adb shell "/system/bin/device_config put activity_manager max_phantom_processes 2147483647" 

# if you want to enable it again
# adb shell "/system/bin/device_config put activity_manager max_phantom_processes 32"
```

- Android 12, GMS

```shell
./adb shell "/system/bin/device_config set_sync_disabled_for_tests persistent; /system/bin/device_config put activity_manager max_phantom_processes 2147483647"

# if you want to enable it again
# ./adb shell "/system/bin/device_config set_sync_disabled_for_tests persistent; /system/bin/device_config put activity_manager max_phantom_processes 32"
```

[ref:Phantom, Cached And Empty Processes](https://github.com/agnostic-apollo/Android-Docs/blob/master/en/docs/apps/processes/phantom-cached-and-empty-processes.md)

[ref:Termux防止杀后台 解决signal 9错误](https://www.bilibili.com/read/cv20060713/)