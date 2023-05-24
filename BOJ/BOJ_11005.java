import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {
			BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
			BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
	
			StringTokenizer st = new StringTokenizer(br.readLine());
			int n = Integer.parseInt(st.nextToken());
			int b = Integer.parseInt(st.nextToken());
	
			StringBuilder sb = new StringBuilder();

			while(n>0) {
				
				int remainer = n%b;
				
				if(remainer>=10) {
					sb.insert(0, (char) (remainer+55));	
				} else {
					sb.insert(0, remainer);
				}
				n /= b;
				
			}

			bw.write(sb.toString());
			
			bw.flush();
			bw.close();
			
	}
}
