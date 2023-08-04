import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.util.Stack;

public class Main {

	public static void main(String[] args) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
		BufferedWriter bw = new BufferedWriter(new OutputStreamWriter(System.out));

		int num = Integer.parseInt(br.readLine());

		Stack<Integer> stack = new Stack<>();
		while(num-->0) {
			int i = Integer.parseInt(br.readLine());
			if(i!=0) {
				stack.add(i);
			} else {
				stack.remove(stack.size()-1);
			}
		}
		
		br.close();
		
		int sum = 0;
		
		for(int i=0; i<stack.size(); i++) {
			sum += stack.get(i);
		}
		
		bw.write(sum+"");
		bw.flush();
		bw.close();
	}

}
