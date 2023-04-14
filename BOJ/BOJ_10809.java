import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.List;

public class Main {
	public static void main(String[] args) throws IndexOutOfBoundsException, IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
	
		
		String s = br.readLine();
		
		for(int i=0; i<26; i++) {
			int k = 0;
			for(int j=0; j<s.length(); j++) {
				if(s.charAt(j)==(i+97)) {
					k=1;
					bw.write(j + " ");
					break;
				}
			} if(k!=1) {bw.write(-1 + " ");}
		}
		
		bw.flush();
		bw.close();
		
	}
}
