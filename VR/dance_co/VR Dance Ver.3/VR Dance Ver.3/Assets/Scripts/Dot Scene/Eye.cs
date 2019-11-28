using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Eye : MonoBehaviour
{
    public GameObject cameras, GameManager;
    public GameObject eye1, eye2;
    public GameObject up1, up2;
    public GameObject down1, down2;

    GameObject eyeCopy1, eyeCopy2;
    Circle circle;
    Flat flat;
    ColorCircle cCircle;

    public bool isBlink, time10;
    bool isLeft, isRight, isDot, BlinkFinish;
    bool down, eyeTouch, eyeCopy;
    bool gotoDot, scale;
    bool cMoveStart, ccCtorus, hMove;
    bool timeCoroutine;
    
    public float speed, time;

    void Start()
    {
        circle = GameObject.Find("CircleManager").GetComponent<Circle>();
        cCircle = GameObject.Find("ColorCircleManager").GetComponent<ColorCircle>();
        flat = GameObject.Find("FlatManager").GetComponent<Flat>();
        eye2.SetActive(false);
        time10 = isBlink = false;
        isLeft = isRight = eyeTouch = gotoDot = false;
        down = eyeCopy = scale = isDot = BlinkFinish = false;
        speed = 1.0f;
        time = 0.0f;
        timeCoroutine = false;
    }

    void Update()
    {
        if(time10 && !eyeTouch)
        {
            if(!timeCoroutine)
            {
                StartCoroutine(timeChecker());
                timeCoroutine = true;
            }

            eye1.transform.SetParent(cameras.transform);
            up1.transform.localRotation = Quaternion.Slerp(up1.transform.localRotation,
                    Quaternion.Euler(-10f, 0, 0), speed * Time.deltaTime);
            down1.transform.localRotation = Quaternion.Slerp(down1.transform.localRotation,
                    Quaternion.Euler(-140f, 0, 0), speed * Time.deltaTime);

            if (up1.transform.localRotation.eulerAngles.x >= 345f && up1.transform.localRotation.eulerAngles.x <= 355f &&
                    down1.transform.localRotation.eulerAngles.x >= 315f && down1.transform.localRotation.eulerAngles.x <= 325f)
            {
                up1.transform.localRotation = Quaternion.Euler(-10f, 0, 0);
                up2.transform.localRotation = Quaternion.Euler(-10f, 0, 0);
                down1.transform.localRotation = Quaternion.Euler(-140f, 0, 0);
                down2.transform.localRotation = Quaternion.Euler(-140f, 0, 0);
                eyeTouch = true;
            }
        }

        if (!isLeft && eyeTouch)
        {
            eye1.transform.LookAt(cameras.transform);

            eye1.transform.localPosition = Vector3.MoveTowards(eye1.transform.localPosition,
                new Vector3(-0.216f, 0, 0.542f), 1.0f * Time.deltaTime);

            if (eye1.transform.localPosition == new Vector3(-0.216f, 0, 0.542f))
            {
                eye2.transform.localPosition = eye1.transform.localPosition;
                isLeft = true;
            }
        }

        if (isLeft && !isRight)
        {
            eye1.transform.LookAt(cameras.transform);
            eye2.transform.LookAt(cameras.transform);

            eye2.SetActive(true);
            eye2.transform.localPosition = Vector3.MoveTowards(eye2.transform.localPosition,
                new Vector3(0.19f, 0, 0.54f), 0.3f * Time.deltaTime);

            if (eye2.transform.localPosition == new Vector3(0.19f, 0, 0.54f))
            {
                isRight = true;
            }
        }

        if (isRight && !BlinkFinish)
        {
            eye1.transform.LookAt(cameras.transform);
            eye2.transform.LookAt(cameras.transform);

            if (!down)
            {
                up1.transform.localRotation = Quaternion.Slerp(up1.transform.localRotation,
                    Quaternion.Euler(10f, 0, 0), 5.0f * Time.deltaTime);
                up2.transform.localRotation = Quaternion.Slerp(up2.transform.localRotation,
                    Quaternion.Euler(10f, 0, 0), 5.0f * Time.deltaTime);
                down1.transform.localRotation = Quaternion.Slerp(down1.transform.localRotation,
                    Quaternion.Euler(-180f, 0, 0), 5.0f * Time.deltaTime);
                down2.transform.localRotation = Quaternion.Slerp(down2.transform.localRotation,
                    Quaternion.Euler(-180f, 0, 0), 5.0f * Time.deltaTime);

                if(up1.transform.localRotation.eulerAngles.x >= 8f && up1.transform.localRotation.eulerAngles.x <= 13f)
                {
                    up1.transform.localRotation = Quaternion.Euler(10f, 0, 0);
                    up2.transform.localRotation = Quaternion.Euler(10f, 0, 0);
                    down1.transform.localRotation = Quaternion.Euler(-180f, 0, 0);
                    down2.transform.localRotation = Quaternion.Euler(-180f, 0, 0);
                    down = true;
                }
            }

            else
            {
                up1.transform.localRotation = Quaternion.Slerp(up1.transform.localRotation,
                    Quaternion.Euler(-10f, 0, 0), 5.0f * Time.deltaTime);
                up2.transform.localRotation = Quaternion.Slerp(up2.transform.localRotation,
                    Quaternion.Euler(-10f, 0, 0), 5.0f * Time.deltaTime);
                down1.transform.localRotation = Quaternion.Slerp(down1.transform.localRotation,
                    Quaternion.Euler(-140f, 0, 0), 5.0f * Time.deltaTime);
                down2.transform.localRotation = Quaternion.Slerp(down2.transform.localRotation,
                    Quaternion.Euler(-140f, 0, 0), 5.0f * Time.deltaTime);

                if (up1.transform.localRotation.eulerAngles.x >= 350f && up1.transform.localRotation.eulerAngles.x <= 352f)
                {
                    up1.transform.localRotation = Quaternion.Euler(-10f, 0, 0);
                    up2.transform.localRotation = Quaternion.Euler(-10f, 0, 0);
                    down1.transform.localRotation = Quaternion.Euler(-140f, 0, 0);
                    down2.transform.localRotation = Quaternion.Euler(-140f, 0, 0);
                    Invoke("DownFalse", 1.0f);
                }
            }
        }

        if (isDot)
        {
            if (up1.transform.localRotation.eulerAngles.x >= 350f && up1.transform.localRotation.eulerAngles.x <= 352f)
            {
                BlinkFinish = true;
            }
        }

        if (isDot && BlinkFinish)
        {
            if (!eyeCopy)
            {
                eyeCopy1 = Instantiate(eye1);
                eyeCopy2 = Instantiate(eye2);
                eyeCopy1.transform.SetParent(cameras.transform);
                eyeCopy2.transform.SetParent(cameras.transform);
                eyeCopy1.transform.localPosition = eye1.transform.localPosition;
                eyeCopy1.transform.localRotation = eye1.transform.localRotation;
                eyeCopy2.transform.localPosition = eye2.transform.localPosition;
                eyeCopy2.transform.localRotation = eye2.transform.localRotation;
                eyeCopy = true;
                eyeCopy1.transform.SetParent(GameManager.transform);
                eyeCopy2.transform.SetParent(GameManager.transform);
            }

            eyeCopy1.transform.LookAt(cameras.transform);
            eyeCopy2.transform.LookAt(cameras.transform);
            eye1.transform.LookAt(cameras.transform);
            eye2.transform.LookAt(cameras.transform);

            eyeCopy1.transform.localPosition = Vector3.MoveTowards(eyeCopy1.transform.localPosition,
                new Vector3(-1, 1.8f, -3), 0.5f * Time.deltaTime);
            eyeCopy2.transform.localPosition = Vector3.MoveTowards(eyeCopy2.transform.localPosition,
                new Vector3(-1, 1.8f, -2.6f), 0.5f * Time.deltaTime);

            eye1.transform.localPosition = Vector3.MoveTowards(eye1.transform.localPosition,
                new Vector3(0, 0.112f, 0.518f), 0.5f * Time.deltaTime);
            eye2.transform.localPosition = Vector3.MoveTowards(eye2.transform.localPosition,
                new Vector3(0, 0.112f, 0.518f), 0.5f * Time.deltaTime);

            if(eye1.transform.localPosition == new Vector3(0, 0.112f, 0.518f))
            {
                eye2.SetActive(false);
            }

            if (eyeCopy1.transform.localPosition == new Vector3(-1, 1.8f, -3))
            {
                gotoDot = true;
                isDot = false;
            }
        }

        if(gotoDot)
        {
            eye1.transform.SetParent(GameManager.transform);
            eyeCopy1.transform.LookAt(cameras.transform);
            eyeCopy2.transform.LookAt(cameras.transform);

            up1.transform.localRotation = Quaternion.Slerp(up1.transform.localRotation,
                    Quaternion.Euler(new Vector3(11f, 0, 0)), speed * Time.deltaTime);
            down1.transform.localRotation = Quaternion.Slerp(down1.transform.localRotation,
                    Quaternion.Euler(new Vector3(-185f, 0, 0)), speed * Time.deltaTime);

            eye1.transform.position = Vector3.MoveTowards(eye1.transform.position,
                new Vector3(0, 1f, -1), 0.7f * Time.deltaTime);

            if(!scale)
            {
                StartCoroutine(scales());
                scale = true;
            }

            if(eye1.transform.position == new Vector3(0,1f,-1))
            {
                isBlink = true;
                gotoDot = false;
            }
        }

        if(isBlink)
        {
            eye1.SetActive(false);
            eyeCopy1.transform.LookAt(cameras.transform);
            eyeCopy2.transform.LookAt(cameras.transform);
        }

        if(circle.moveStart && !cMoveStart)
        {
            eyeCopy1.transform.localPosition = Vector3.MoveTowards(eyeCopy1.transform.localPosition,
                new Vector3(-1.234f, 0.873f, -2.69f), 1.0f * Time.deltaTime);
            eyeCopy2.transform.localPosition = Vector3.MoveTowards(eyeCopy2.transform.localPosition,
                new Vector3(-0.79f, 0.99f, -2.7f), 1.0f * Time.deltaTime);

            if(eyeCopy1.transform.localPosition == new Vector3(-1.234f, 0.873f, -2.69f))
            {
                cMoveStart = true;
            }
        }

        if(cCircle.Ctorus && !ccCtorus)
        {
            eyeCopy1.transform.localPosition = Vector3.MoveTowards(eyeCopy1.transform.localPosition,
                new Vector3(-0.143f, 0.787f, -1.23f), 1.0f * Time.deltaTime);
            eyeCopy2.transform.localPosition = Vector3.MoveTowards(eyeCopy2.transform.localPosition,
                new Vector3(0.3f, 0.787f, -1.24f), 1.0f * Time.deltaTime);

            if (eyeCopy1.transform.localPosition == new Vector3(-0.143f, -0.787f, -1.23f))
            {
                ccCtorus = true;
            }
        }
    }

    void DownFalse()
    {
        down = false;
    }

    IEnumerator scales()
    {
        bool scaled = false;
        Vector3 size = new Vector3(-0.001f, -0.001f, -0.001f);
        while (!scaled)
        {
            eye1.transform.localScale += size;

            if(eye1.transform.localScale.x <= 0.05f)
            {
                scaled = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }

    IEnumerator timeChecker()
    {
        while (!isDot)
        {
            time += 0.01f;

            if (time >= 30f)
            {
                isDot = true;
            }

            yield return new WaitForSeconds(0.01f);
        }
    }
}
