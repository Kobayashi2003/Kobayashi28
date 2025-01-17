import java.io.*;

public class FileStringTest2 {
    public static void main(String[] args) throws IOException {
        
        File f = new File("test.txt");

        FileOutputStream fop = new FileOutputStream(f);

        OutputStreamWriter writer = new OutputStreamWriter(fop, "UTF-8");
        writer.append("中文");
        writer.append("\r\n");
        writer.append("English");
        writer.close();

        fop.close();

        FileInputStream fip = new FileInputStream(f);

        InputStreamReader reader = new InputStreamReader(fip, "UTF-8");
        StringBuffer sb = new StringBuffer();
        while (reader.ready()) {
            sb.append((char) reader.read());
        }
        System.out.println(sb.toString());
        reader.close();

        fip.close();
    } 
}
