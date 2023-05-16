import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws Exception {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		String s = br.readLine();
		
		int sum=0;
		for(int i=0; i<s.length(); i++) {
			int c = s.charAt(i);

			int time =0;
			switch((c-65)/3) {
				case 0: time=3; break;
				case 1: time=4; break;
				case 2: time=5; break;
				case 3: time=6; break;
				case 4: time=7; break;
				case 5: time=8; break;
				case 6: time=9; break;
				case 7: time=10; break;
				default: time=10;
			}
			
			if(c == 83) {
				time=8;
			}
			if(c == 86) {
				time=9;
			}
			sum+= time;
		}
		bw.write(sum+"");
		bw.flush();
		bw.close();
		
	}
}
