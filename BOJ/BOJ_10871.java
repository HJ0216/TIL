import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.StringTokenizer;

public class Main {
	public static void main(String[] args) throws IOException{
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		StringTokenizer st = new StringTokenizer(br.readLine());

		int n = Integer.parseInt(st.nextToken());
		int x = Integer.parseInt(st.nextToken());

		st = new StringTokenizer(br.readLine());
		// StringTokenizer는 1회만 사용 가능
		// 1행에 n, x를 구분하기 위해 StringTokenizer를 사용했으므로 for문을 위해 재생성 필요
		
		for(int i=0; i<n; i++) {
			int a = Integer.parseInt(st.nextToken());
			if(a<x)
				bw.write(a+" ");
		}
		bw.flush();
		bw.close();
	}
}
