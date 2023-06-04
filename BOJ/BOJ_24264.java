import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
 
public class Main {
    public static void main(String[] args) throws Exception {
 
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
 
        long n = Integer.parseInt(br.readLine());
        
        long result = (long) Math.pow(n, 2);
        
        bw.write(result + "\n" + 2);
        
        bw.flush();
        bw.close();
    }
}
