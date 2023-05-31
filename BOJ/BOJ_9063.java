import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int n = Integer.parseInt(br.readLine());

		int maxA = -10000;
		int minA = 10000;
		int maxB = -10000;
		int minB = 10000;
		for(int i=0; i<n; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine(), " ");
			int a = Integer.parseInt(st.nextToken());
			if(a>maxA) {maxA=a;}
			if(a<minA) {minA=a;}
			int b = Integer.parseInt(st.nextToken());
			if(b>maxB) {maxB=b;}
			if(b<minB) {minB=b;}			
		}
		
		bw.write((maxA-minA)*(maxB-minB)+"");
				
		bw.flush();
		bw.close();

	}
}
