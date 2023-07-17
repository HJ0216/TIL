import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;

public class Main {
	public static void main(String[] args) throws IndexOutOfBoundsException, IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		String s = br.readLine();

		String[] strArr = { "c=", "c-", "dz=", "d-", "lj", "nj", "s=", "z=" };

		for (int i = 0; i < strArr.length; i++) {
			if(s.contains(strArr[i])) {
				s = s.replace(strArr[i], "1");
			}
		}
		
		bw.write(s.length()+"");
		
		bw.flush();
		bw.close();

	}
}
