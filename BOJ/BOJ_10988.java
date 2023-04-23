import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		
		String s = br.readLine();
		
		int sw=1;
		for(int i=0; i<(s.length()/2); i++){
			if(s.charAt(i)!=(s.charAt(s.length()-(1+i)))) {
				sw=0;
			}
		}
		bw.write(sw+"");
		bw.flush();
		bw.close();
	}
}
