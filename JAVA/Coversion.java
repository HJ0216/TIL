public class Coversion {

	public static void main(String[] args) {
//		byte by = 128;
//		System.out.println(by);

		// Type mismatch: cannot convert from int to byte
		// -> byte가 다룰 수 있는 범위를 넘어설 경우, int->byte로 변환할 수 없다는 오류메세지 발생

		byte by2 = (byte) 129;
		System.out.println(by2); // by2 = -127
		// literal 앞에 변수 타입을 함께 적어주면 값 손실 발생(최대값+1=최소값 형식)
		// 최대값 127를 넘어가면 최소값 -128에서 다시 계산


		System.out.println(10/4.0f); // 2.5(int/float=float)
		// 타입이 다른 피연산자의 계산은 값 손실을 최소화하며 진행됨
		// * 단, 피연산자가 int보다 작은 형태일 경우, 모두 int로 변환하여 계산
		
	}

}
