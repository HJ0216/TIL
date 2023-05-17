import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine(), " ");
		int a = Integer.parseInt(st.nextToken());
		int b = Integer.parseInt(st.nextToken());
		int c = Integer.parseInt(st.nextToken());
		
		if(a>b && a>c) {
			if(b+c>a) {bw.write((a+b+c)+"");}
			else {bw.write((b+c)*2 - 1 + "");}
		} else if(b>a && b>c) {
			if(a+c>b) {bw.write((a+b+c)+"");}
			else {bw.write((a+c)*2 - 1 + "");}
		} else {
			if(a+b>c) {bw.write((a+b+c)+"");}
			else {bw.write((a+b)*2 - 1 + "");}
			
		}
		
		bw.flush();
		bw.close();
		
	}
}
