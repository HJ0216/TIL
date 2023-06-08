import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.math.BigInteger;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));


		int[][] intArr = new int[9][9];
		int intMax = intArr[0][0];
		
		int iMax=0;
		int jMax=0;
		for(int i=0; i<9; i++) {
			StringTokenizer st = new StringTokenizer(br.readLine(), " ");
			for(int j=0; j<9; j++) {
				intArr[i][j] = Integer.parseInt(st.nextToken());
				if(intArr[i][j] >= intMax) {
					intMax = intArr[i][j];
					iMax = i+1;
					jMax = j+1;
				}
			}
		}
		
		bw.write(intMax + " " + iMax + " " + jMax);
		bw.flush();
	}
}
