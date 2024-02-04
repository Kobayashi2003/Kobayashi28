import java.io.File;

public class DirList {
    public static void main(String[] args) {
        String dirname = "../";
        File f = new File(dirname);
        if (f.isDirectory()) {
            System.out.println("directory: " + dirname);
            String s[] = f.list();
            for (int i = 0; i < s.length; ++i) {
                File f_sub = new File(dirname + "/" + s[i]);
                if (f_sub.isDirectory())
                    System.out.println(s[i] + " is a directory");
                else 
                    System.out.println(s[i] + " is a file");
            }
        } else {
            System.out.println(dirname + " is not a directory");
        }
    } 
}
