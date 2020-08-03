using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Test : MonoBehaviour
{
    bool a, d;
    bool b, c;

    void Start()
    {
        a = d = false;
        b = c = false;
    }

    void Update()
    {
        if(!a)
        {
            iTweenMove();
            a = true;
        }

        if(b && !d)
        {
            iTweenMove2();
            d = true;
        }

        gameObject.transform.Rotate(Vector3.up * 25f * Time.deltaTime);
    }

    void iTweenMove()
    {
        iTween.MoveTo(gameObject, iTween.Hash("path", iTweenPath.GetPath("ArrowPath"),
            "time", 7, "easeType", iTween.EaseType.linear, "oncomplete", "bTrue",
            "oncompletetarget", gameObject));
    }

    void iTweenMove2()
    {
        iTween.MoveTo(gameObject, iTween.Hash("path", iTweenPath.GetPath("ArrowPath2"),
            "time", 7, "easeType", iTween.EaseType.linear));
    }

    void bTrue()
    {
        b = true;
    }
}
