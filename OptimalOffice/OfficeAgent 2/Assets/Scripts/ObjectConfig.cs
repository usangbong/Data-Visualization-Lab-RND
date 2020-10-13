using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ObjectConfig : MonoBehaviour
{
    //Object의 크기
    public float horizontalLength;
    public float verticalLength;

    //Snape 여부
    public bool isHorizontalSnap = false;
    public bool isVerticalSnap = false;

    //Object는 중심점을 기준으로 존재하므로 원래 길이 / 2
    public float getHorizontalLength() { return horizontalLength / 2f; }
    public float getVerticalLength() { return verticalLength / 2f; }
}
