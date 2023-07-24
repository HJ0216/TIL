import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		
		int num = Integer.parseInt(br.readLine());
		int num2 = num;
		
		int cnt = 2;
		while(cnt<=num){
			if(num2%cnt==0) {
				bw.write(cnt + "\n");
				num2 /= cnt;
				if(num2==1) {
					break;					
				}
			} else {
				cnt++;
			}
		}
		
		bw.flush();
		bw.close();
		
	}
	
}
