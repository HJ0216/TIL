import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		
		int t = Integer.parseInt(br.readLine());
		for(int i=0; i<t; i++) {
			for(int j=(t-i-1); j>0; j--) {
				bw.write(" ");
			}
			for(int j=0; j<2*i+1; j++) {
				bw.write("*");
			}
			bw.write("\n");
		} // for_outer
		
		for(int i=0; i<t-1; i++) {
			for(int j=0; j<i+1; j++) {
				bw.write(" ");
			}
			for(int j=2*(t-i-1)-1; j>0; j--) {
				bw.write("*");
			}
			bw.write("\n");
		} // for_outer
		
		bw.flush();
		bw.close();
		
	}
	
}
