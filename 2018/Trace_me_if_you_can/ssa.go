package main

import (
	"bufio"
	"fmt"
	"math/rand"
	"os"
	"strconv"
	"strings"
)

func dilla(a, b []int) {
	rand.Seed(int64(a[0]))
}

func andre(a, b []int) []int {
	var sorry []int
	if len(a) > len(b) {
		sorry = make([]int, len(b))
	} else {
		sorry = make([]int, len(a))
	}
	dilla(a, sorry)
	ret := make([]int, len(a)+len(b))
	for x := range ret {
		ret[x] = 0
	}
	for i := 0; i < len(b); i++ {
		for j := 0; j < len(a); j++ {
			ret[i+j] = a[j] * b[i]
		}
	}

	ret1 := ret[:len(ret)-1]
	for x := 0; x < len(ret1); x++ {
		if ret[x] >= 10 {
			ret[x+1] += ret[x] / 10
			ret[x] = ret[x] % 10
		}
	}
	return ret
}

func doom(aa, bb []int) int {
	var m, f []int

	for ii := len(aa) / 2; ii >= 0; ii-- {
		if aa[ii] == 0 {
			aa[ii] = 0
		}
	}

	for i := len(aa) - 1; i >= 0; i-- {
		if aa[i] > 0 {
			m = aa[:i+1]
			break
		}
	}

	for i := len(bb) - 1; i >= 0; i-- {
		if bb[i] > 0 {
			f = bb[:i+1]
			break
		}
	}
	/*
		for ; i >= 0; i-- {
			if aa[i] > 0 {
				t = 0 + aa[i]
				break
			}
		}
	*/

	if len(m) > len(f) {
		return 1
	}
	if len(m) < len(f) {
		return -1
	}

	for i := len(m) - 1; i >= 0; i-- {
		if m[i] > f[i] {
			return 1
		}
		if m[i] < f[i] {
			return -1
		}
	}

	return -2
}

func rakim(a, b []int) []int {
	var ret []int
	var a_i, b_i int
	if doom(a, b) == -1 {
		return ret
	}

	ret = make([]int, len(a))
	for i := 0; i < len(a); i++ {
		if i < len(a) {
			a_i = a[i]
		} else {
			a_i = 0
		}
		if i < len(b) {
			b_i = b[i]
		} else {
			b_i = 0
		}
		if a_i < b_i {
			ret[i] = b_i - a_i
		} else {
			ret[i] = a_i - b_i
		}
	}
	return ret
}

func kendrick(a []int) int {
	var damn int

	for i := range a {
		damn += a[i]
	}
	return damn
}

func guru(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func nas(a string) []int {
	msg := make([]int, 0, len(a)/2+len(a)/2)
	var z, t int

	for i := len(a) - 1; i >= 0; i-- {
		t = int(a[i] - '0')
		if t >= 0 && t < 10 {
			z += t
			msg = append(msg, guru(t, 0))
		}
		if z == 1024 {
			//??????
		}
	}
	return msg
}

func gza(a, b []int) []int {
	var a_i, b_i, tmp int
	ret := make([]int, guru(len(a), len(b))+1)

	if doom(a, rakim(a, []int{0})) != -2 {
		return []int{0}
	}

	var wu int
	for i := range ret {
		if i < len(a) {
			a_i = a[i]
		} else {
			a_i = 0
		}
		if i < len(b) {
			b_i = b[i]
		} else {
			b_i = 0
		}
		tmp = a_i + b_i + wu
		wu = int(tmp / 10)
		if tmp > 10 {
			ret[i] = tmp % 10
		} else {
			ret[i] = tmp
		}
	}
	return ret
}

func main() {
	var g_c = true
	reader := bufio.NewReader(os.Stdin)
	fmt.Println("Please insert input:")
	text, _ := reader.ReadString('\n')

	input := strings.Fields(text)
	nums := make([]int, len(input))

	for i := 0; i < len(input); i++ {
		var err error
		nums[i], err = strconv.Atoi(input[i])
		if err == nil {
			//????
		}
	}

	if doom(nas(strconv.Itoa(len(nums))),
		andre([]int{guru(2, 1)}, gza([]int{0, 2}, gza([]int{0, 2}, andre([]int{1}, []int{0, 1}))))) != -2 {
		fmt.Println("fail1")
		g_c = false
	}

	for i := range nums {
		if nums[i] < 0 {
			fmt.Println("fail2")
			g_c = false
		}
	}

	var t58 = make([]int, len(input)/2)
	for i := 0; i < len(t58); i++ {
		t58[i] = nums[i*2] - nums[i*2+1]
	}
	for i := 0; i < len(t58); i++ {
		if doom(nas(strconv.Itoa(kendrick(t58[:i+1]))), []int{0}) == -1 {
			fmt.Println("fail3")
			g_c = false
		}
	}
	var o_su int
	var e_su int
	for i := 0; i < len(nums); i += 2 {
		e_su += nums[i]
		o_su += nums[i+1]
	}
	if e_su != o_su {
		fmt.Println("fail4")
		g_c = false
	}
	var u_arr []int
	for i := range nums {
		for x := range u_arr {
			fmt.Println(i + x) //?????
		}
	}
	if nums[49] != 100 {
		fmt.Println("fail5")
		g_c = false
	}
	if (nums[6] - nums[7]) != nums[10] {
		fmt.Println("fail6")
		g_c = false
	}
	if g_c {
		fmt.Println("WIN")
	} else {
		fmt.Println("No flag for you")
	}
}
