/* author: lyn
date: 2018/12/7
name: LOL_Img
*/

package main

import (
	"fmt"
	"github.com/json-iterator/go"
	"io/ioutil"
	"net/http"
	"os"
	"regexp"
	"runtime"
	"sync"
)

const baseUrl = "http://ossweb-img.qq.com/images/lol/web201310/skin/big"

func main() {
	runtime.GOMAXPROCS(10)
	var wg sync.WaitGroup
	data, err := readJson("./lol_hero.json")
	if err != nil {
		fmt.Println("失败")
	}
	func() {
		for _, name := range data {
			wg.Add(1)
			go getHeroImageIds(name, &wg)
		}
	}()
	wg.Wait()
}

func readJson(fileName string) (data map[int]string, err error) {
	body, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Println("读取文件出错")
		return nil, nil
	}
	err = jsoniter.Unmarshal(body, &data)
	if err != nil {
		fmt.Println("转换文件出错，", err)
		return nil, nil
	}
	return data, nil
}

func requests(url string) (body []byte) {
	client := &http.Client{}
	request, _ := http.NewRequest("GET", url, nil)
	if response, reqErr := client.Do(request); reqErr != nil {
		defer response.Body.Close()
		fmt.Printf("请求出错, 错误原因为 %s", reqErr)
		panic("请求出错")
	} else {
		defer response.Body.Close()
		body, _ := ioutil.ReadAll(response.Body)
		return body
	}
}

func getHeroImageIds(heroName string, wg *sync.WaitGroup) {
	var wg2 sync.WaitGroup
	defer func() {
		wg.Done()
		err := recover()
		if err != nil {
			fmt.Println(err)
			return
		}
	}()
	var skinList []map[string]interface{}
	heroJsUrl := fmt.Sprintf("https://lol.qq.com/biz/hero/%s.js", heroName)
	body := requests(heroJsUrl)
	com := regexp.MustCompile(`"skins":(.*?),"info"`)
	temp := com.FindSubmatch(body)
	err := jsoniter.Unmarshal(temp[1], &skinList)
	checkErr(err, "解压js文件出错")
	for _, elem := range skinList {
		skinName := elem["name"].(string)
		skinId := elem["id"].(string)
		fmt.Printf("已得到: %s-%s, 开始保存文件。。。\n", heroName, skinName)
		wg2.Add(1)
		go downloadAndSaveImages(skinId, skinName, heroName, &wg2)
	}
	wg2.Wait()
}

func checkErr(err error, msg string) {
	if err != nil {
		fmt.Println(err, msg)
		panic(msg)
	}
}

func replaceName(srcName string) (targetName string) {
	compile := regexp.MustCompile(`[\\/:*?"<>|]`)
	targetName = compile.ReplaceAllString(srcName, "")
	return
}

func downloadAndSaveImages(id, skinName, heroName string, wg2 *sync.WaitGroup) {
	defer func() {
		wg2.Done()
		err := recover()
		if err != nil {
			fmt.Println(err)
			return
		}
	}()
	heroSkinUrl := baseUrl + id + ".jpg"
	skinName = replaceName(skinName)
	imageDir := fmt.Sprintf("./lolimg/%s", heroName)
	err := os.MkdirAll(imageDir, 0644)
	checkErr(err, fmt.Sprintf("创建文件夹%s失败\n", heroName))
	file, err := os.OpenFile(imageDir+"/"+skinName+".jpg", os.O_CREATE|os.O_WRONLY, 0644)
	checkErr(err, fmt.Sprintf("创建文件%s失败\n", skinName+".jpg"))
	body := requests(heroSkinUrl)
	_, err = file.Write(body)
	checkErr(err, "图片写入文件失败\n")
	_ = file.Close()
	fmt.Println(heroName, "-", skinName, "保存成功")
}
