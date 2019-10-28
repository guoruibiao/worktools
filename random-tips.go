package main
/**
 * 使用方法：
 * 
 * 创建/tmp/tips.txt文件，每行内容格式如下：
 *     title_balabala | content_balabala
 *     即 title部分 |（竖线是分隔符） content部分
 * 然后执行：
 *     go run random-tips.go
 * 拓展：
 *     添加flags支持，让提示文件内容变得可选路径
 **/
import (
	"bufio"
	"fmt"
	"github.com/guoruibiao/commands"
	"io"
	"os"
	"strings"
	"time"
)

type Tip struct {
	title   string
	content string
}

var TIP_MAP []Tip = []Tip{
	Tip{"健康小贴士", "该喝水了"},
	Tip{"生活小贴士", "每天吃两个核桃，有助于提高记忆力"},
	Tip{"xx小贴士", "两年学说话，一生学闭嘴"},
	Tip{"天气小贴士", "是时候穿上秋裤了"},
}

func getFileContents(filepath string) {
	file, err := os.Open(filepath)
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	defer file.Close()
	reader := bufio.NewReader(file)
	for {
		linebytes, _, err := reader.ReadLine()
		if err == io.EOF {
			break
		}
		line := string(linebytes)
		tipArray := strings.Split(line, "|")
		//fmt.Println(line, tipArray, len(tipArray))
		if len(tipArray) == 2 {
			// 根据分隔符进行截取，拼装到tips数组里面
			TIP_MAP = append(TIP_MAP, Tip{tipArray[0], tipArray[1]})
		}
	}
}

func generateTip() (Tip, error) {
	index := int(time.Now().Unix()) % len(TIP_MAP)
	return TIP_MAP[index], nil
}

func main() {
	getFileContents("/tmp/tips.txt")
	tip, _ := generateTip()
	commander := commands.New()
	command := fmt.Sprintf(`display notification "%s" with title "%s"`, tip.content, tip.title)
	//fmt.Println("command=", command)
	commander.Run("osascript", "-e", command)
}
