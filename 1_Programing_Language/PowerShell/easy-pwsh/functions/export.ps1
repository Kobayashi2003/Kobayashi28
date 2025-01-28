function export($name, $value) {
    set-item -force -path "env:$name" -value $value;
}