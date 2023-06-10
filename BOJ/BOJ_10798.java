import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {

		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		char[][] charArr = new char[5][15];
		int maxLength = 0;
		
		for(int i=0; i<5; i++) {
			String s = br.readLine();
			maxLength = Math.max(maxLength, charArr[i].length);
			for(int j=0; j<s.length(); j++)
				charArr[i][j] = s.charAt(j);
		}

		StringBuilder sb = new StringBuilder();

		for (int i=0; i<maxLength; i++) {
			for (int j=0; j<5; j++) {
		        if (charArr[j][i] == '\0') {
		        	continue;
		        }
		        sb.append(charArr[j][i]);
		    }
		}

		bw.write(sb.toString());
		
		bw.flush();
	}
}
