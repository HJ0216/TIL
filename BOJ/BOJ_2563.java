import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));

		int n = Integer.parseInt(br.readLine());

		boolean[][] bArr = new boolean[100][100];
		
		for (int i = 0; i < n; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine());

			int intX = Integer.parseInt(st.nextToken());
			int intY = Integer.parseInt(st.nextToken());
			
			for(int j = 0; j<10; j++) {
				for(int k=0; k<10; k++) {
					bArr[intX-1+j][intY-1+k] = true;					
				}
				
			}

		}
		
		int cntXY = 0;
		for(int i=0; i<100; i++) {
			for(int j=0; j<100; j++) {
				if(bArr[i][j]) {
					cntXY++;
				}				
			}
		}

		bw.write(cntXY + "\n");

		bw.flush();
		bw.close();

	}

}
