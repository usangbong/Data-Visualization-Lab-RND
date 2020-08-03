using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class MakeFigure : MonoBehaviour
{
    public GameObject Figure, Line1, Line2, Danger;
    public GameObject Line3, Line4, Line5, Ikinema;
    public GameObject col1, col2, col3, col4;
    public GameObject Arrows, Spring, nullPar;

    public Material black, blue, yellow, green, orange, brown, white, beige;

    public bool isColliding, makeArrow, FigureFin;
    public bool collider1, collider2, arr, MakeStart;

    bool timeFunc;

    int figNum, matNum;
    int figCnt, matCnt;
    bool scale, rand;
    bool makingArrow;
    bool ivk;

    public float time;
    bool timeFin;
    
    List<Material> matList = new List<Material>();

    List<bool> figureList = new List<bool>();
    List<bool> matListBool = new List<bool>();

    Vector3 upPos, downPos;
    Vector3 scales;

    Linear linear;

    void Start()
    {
        time = 0;
        timeFin = false;
        scales = new Vector3(0, 0, 0.01f);
        timeFunc = FigureFin = MakeStart = false;
        makingArrow = arr = ivk = false;

        for (int i = 0; i < 8; i++)
        {
            figureList.Add(false);
            matListBool.Add(false);
        }

        matList.Add(black);
        matList.Add(blue);
        matList.Add(yellow);
        matList.Add(green);
        matList.Add(orange);
        matList.Add(brown);
        matList.Add(white);
        matList.Add(beige);

        col1.SetActive(false);
        col2.SetActive(false);
        col3.SetActive(false);
        col4.SetActive(false);
        Line3.SetActive(false);
        Line4.SetActive(false);
        Line5.SetActive(false);

        linear = GameObject.Find("LinearManager").GetComponent<Linear>();
        figNum = matNum = -1;
        figCnt = matCnt = 0;

        isColliding = makeArrow = scale = false;
        collider1 = collider2 = rand = false;

        upPos = new Vector3(0, 0, 0.005f);
        downPos = new Vector3(0, 0, -0.005f);
    }

    void Update()
    {
        if(linear.arrowDown && !makeArrow && MakeStart)
        {
            linear.shortLinear2.SetActive(false);
            Line1.transform.SetParent(Figure.transform);
            Line2.transform.SetParent(Figure.transform);
            Line1.GetComponent<MeshRenderer>().material = matList[linear.matNum];
            Line2.GetComponent<MeshRenderer>().material = matList[linear.matNum];
            Line3.GetComponent<MeshRenderer>().material = matList[linear.matNum];
            Line4.GetComponent<MeshRenderer>().material = matList[linear.matNum];
            Line5.GetComponent<MeshRenderer>().material = matList[linear.matNum];
            Line3.transform.position = new Vector3(0.2f, 0.924f, -0.136f);
            Line3.transform.rotation = Quaternion.Euler(-45, 90, 0);
            Line3.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            Line4.transform.position = new Vector3(0.2f, 0.924f, -0.136f);
            Line4.transform.rotation = Quaternion.Euler(-45, 90, 0);
            Line4.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            Line5.transform.position = new Vector3(0.2f, 0.924f, -0.136f);
            Line5.transform.rotation = Quaternion.Euler(-45, 90, 0);
            Line5.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            Ikinema.SetActive(true);
            Line3.SetActive(true);

            makeArrow = true;
        }

        if (isColliding && figCnt < 8)
        {
            if (!rand)
            {
                RandomValue();
                rand = true;
            }

            if(figNum == 0)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(1.4f, 1.54f, -0.05f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(1.4f, 0.9f, -0.02f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(1.4f, 1.25f, 0.34f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(40, 180, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(180, 180, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(-45, 180, 0), 3.0f * Time.deltaTime);

                if(Line1.transform.localScale.z <= 0.1f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }
                
                if(Line2.transform.localScale.z <= 0.7188f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if(Line3.transform.localScale.z <= 0.5f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }

                if(Line1.transform.position == new Vector3(1.4f, 1.54f, -0.05f) &&
                    Line2.transform.position == new Vector3(1.4f, 0.9f, -0.02f) && 
                    Line3.transform.position == new Vector3(1.4f, 1.25f, 0.34f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col1.transform.position = new Vector3(1.4f, 1.465f, -0.15f);
                    col2.transform.position = new Vector3(1.4f, 0.94f, -0.71f);

                    isColliding = false;
                }
            }

            else if(figNum == 1)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);
                Line4.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Line4.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(0.136f, 1.54f, 1), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(0.1f, 0.66f, 1), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(0.8f, 0.74f, 1), 1.0f * Time.deltaTime);
                Line4.transform.position = Vector3.MoveTowards(Line4.transform.position,
                    new Vector3(-0.55f, 1.47f, 1), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(0, 90, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 90 ,0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(90 ,0, 0), 3.0f * Time.deltaTime);
                Line4.transform.rotation = Quaternion.Slerp(Line4.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.7188f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.7188f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.1f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }

                if (Line4.transform.localScale.z <= 0.1f)
                {
                    Line4.transform.localScale += upPos;
                }

                else
                {
                    Line4.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(0.136f, 1.54f, 1) &&
                    Line2.transform.position == new Vector3(0.1f, 0.66f, 1) &&
                    Line3.transform.position == new Vector3(0.8f, 0.74f, 1) &&
                    Line4.transform.position == new Vector3(-0.55f, 1.47f, 1))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(0.825f, 1.465f, 1);
                    col2.transform.position = new Vector3(0.79f, 0.83f, 1);
                    col3.transform.position = new Vector3(-0.55f, 1.336f, 1);
                    col4.transform.position = new Vector3(-0.59f, 0.68f, 1);

                    isColliding = false;
                }

            }

            else if(figNum == 2)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);
                Line4.SetActive(true);
                Line5.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Line4.GetComponent<MeshRenderer>().material = matList[matNum];
                Line5.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(-1.4f, 1.574f, -0.324f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(-1.4f, 0.66f, -0.07f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(- 1.4f, 0.972f, 0.39f), 1.0f * Time.deltaTime);
                Line4.transform.position = Vector3.MoveTowards(Line4.transform.position,
                    new Vector3(-1.4f, 1.745f, -0.041f), 1.0f * Time.deltaTime);
                Line5.transform.position = Vector3.MoveTowards(Line5.transform.position,
                    new Vector3(-1.4f, 1.263f, -0.55f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(-45, 0, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);
                Line4.transform.rotation = Quaternion.Slerp(Line4.transform.rotation,
                    Quaternion.Euler(45, 0, 0), 3.0f * Time.deltaTime);
                Line5.transform.rotation = Quaternion.Slerp(Line5.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.35f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.5f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.33f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }
                if (Line4.transform.localScale.z <= 0.1f)
                {
                    Line4.transform.localScale += upPos;
                }

                else
                {
                    Line4.transform.localScale += downPos;
                }

                if (Line5.transform.localScale.z <= 0.1f)
                {
                    Line5.transform.localScale += upPos;
                }

                else
                {
                    Line5.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(-1.4f, 1.574f, -0.324f) &&
                    Line2.transform.position == new Vector3(-1.4f, 0.66f, -0.07f) &&
                    Line3.transform.position == new Vector3(-1.4f, 0.972f, 0.39f) &&
                    Line4.transform.position == new Vector3(-1.4f, 1.745f, -0.041f) &&
                    Line5.transform.position == new Vector3(-1.4f, 1.263f, -0.55f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(-1.4f, 1.65f, 0.018f);
                    col2.transform.position = new Vector3(-1.4f, 1.28f, 0.4f);
                    col3.transform.position = new Vector3(-1.4f, 1.165f, -0.565f);
                    col4.transform.position = new Vector3(-1.4f, 0.68f, -0.545f);

                    isColliding = false;
                }
            }

            else if(figNum == 3)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);
                Line4.SetActive(true);
                Line5.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Line4.GetComponent<MeshRenderer>().material = matList[matNum];
                Line5.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(0.17f, 1.2f, -1.4f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(-0.07f, 1.32f, -1.4f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(0.19f, 0.635f, -1.4f), 1.0f * Time.deltaTime);
                Line4.transform.position = Vector3.MoveTowards(Line4.transform.position,
                    new Vector3(-0.25f, 0.663f, -1.4f), 1.0f * Time.deltaTime);
                Line5.transform.position = Vector3.MoveTowards(Line5.transform.position,
                    new Vector3(-0.216f, 1.185f, -1.4f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(75, 90 ,0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 90, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(35, 90, 0), 3.0f * Time.deltaTime);
                Line4.transform.rotation = Quaternion.Slerp(Line4.transform.rotation,
                    Quaternion.Euler(-35, 90, 0), 3.0f * Time.deltaTime);
                Line5.transform.rotation = Quaternion.Slerp(Line5.transform.rotation,
                    Quaternion.Euler(-75, 90, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.7f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.7f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.15f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }
                if (Line4.transform.localScale.z <= 0.15f)
                {
                    Line4.transform.localScale += upPos;
                }

                else
                {
                    Line4.transform.localScale += downPos;
                }

                if (Line5.transform.localScale.z <= 0.7f)
                {
                    Line5.transform.localScale += upPos;
                }

                else
                {
                    Line5.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(0.17f, 1.2f, -1.4f) &&
                    Line2.transform.position == new Vector3(-0.07f, 1.32f, -1.4f) &&
                    Line3.transform.position == new Vector3(0.19f, 0.635f, -1.4f) &&
                    Line4.transform.position == new Vector3(-0.25f, 0.663f, -1.4f) &&
                    Line5.transform.position == new Vector3(-0.216f, 1.185f, -1.4f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(0.63f, 1.329f, -1.4f);
                    col2.transform.position = new Vector3(-0.077f, 0.79f, -1.4f);
                    col3.transform.position = new Vector3(-0.74f, 1.316f, -1.4f);
                    col4.transform.position = new Vector3(0.033f, 0.737f, -1.4f);

                    isColliding = false;
                }
            }

            else if(figNum == 4)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(-0.666f, 1.53f, -1.4f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(-0.07f, 1.32f, -1.4f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(-0.845f, 1.267f, -1.4f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(-45, 90, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 90, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(45, 90, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.3f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.5f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.1f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(-0.666f, 1.53f, -1.4f) &&
                    Line2.transform.position == new Vector3(-0.07f, 1.32f, -1.4f) &&
                    Line3.transform.position == new Vector3(-0.845f, 1.267f, -1.4f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col1.transform.position = new Vector3(-0.418f, 0.814f, -1.4f);
                    col2.transform.position = new Vector3(-0.784f, 1.214f, -1.4f);

                    isColliding = false;
                }
            }

            else if(figNum == 5)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);
                Line4.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Line4.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(0.5f, 1.136f, 1), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(0.1f, 0.82f, 1), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(-0.17f, 0.972f, 1), 1.0f * Time.deltaTime);
                Line4.transform.position = Vector3.MoveTowards(Line4.transform.position,
                    new Vector3(0.33f, 0.89f, 1), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(0, 90, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 90, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);
                Line4.transform.rotation = Quaternion.Slerp(Line4.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.3f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.7f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.5f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }
                if (Line4.transform.localScale.z <= 0.3f)
                {
                    Line4.transform.localScale += upPos;
                }

                else
                {
                    Line4.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(0.5f, 1.136f, 1) &&
                    Line2.transform.position == new Vector3(0.1f, 0.82f, 1) &&
                    Line3.transform.position == new Vector3(-0.17f, 0.972f, 1) &&
                    Line4.transform.position == new Vector3(0.33f, 0.89f, 1))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(0.187f, 1.126f, 1);
                    col2.transform.position = new Vector3(-0.58f, 1.13f, 1);
                    col3.transform.position = new Vector3(0.35f, 1.17f, 1);
                    col4.transform.position = new Vector3(0.32f, 1.45f, 1);

                    isColliding = false;
                }
            }

            else if(figNum == 6)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);
                Line4.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Line4.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(-1.4f, 1.17f, 0.18f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(-1.4f, 0.94f, -0.07f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(-1.4f,1.11f, -0.044f), 1.0f * Time.deltaTime);
                Line4.transform.position = Vector3.MoveTowards(Line4.transform.position,
                    new Vector3(-1.4f, 1, -0.136f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(-45, 0, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(90, 0, 0), 3.0f * Time.deltaTime);
                Line4.transform.rotation = Quaternion.Slerp(Line4.transform.rotation,
                    Quaternion.Euler(45, 0, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.355f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.505f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.15f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }
                if (Line4.transform.localScale.z <= 0.1f)
                {
                    Line4.transform.localScale += upPos;
                }

                else
                {
                    Line4.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(-1.4f, 1.17f, 0.18f) &&
                    Line2.transform.position == new Vector3(-1.4f, 0.94f, -0.07f) &&
                    Line3.transform.position == new Vector3(-1.4f, 1.11f, -0.044f) &&
                    Line4.transform.position == new Vector3(-1.4f, 1, -0.136f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(-1.4f, 1.26f, -0.037f);
                    col2.transform.position = new Vector3(-1.4f, 1.654f, -0.036f);
                    col3.transform.position = new Vector3(-1.4f, 1.1f, -0.205f);
                    col4.transform.position = new Vector3(-1.476f, 1.525f, -0.633f);

                    isColliding = false;
                }
            }

            else if(figNum == 7)
            {
                Line1.SetActive(true);
                Line2.SetActive(true);
                Line3.SetActive(true);

                Line1.GetComponent<MeshRenderer>().material = matList[matNum];
                Line2.GetComponent<MeshRenderer>().material = matList[matNum];
                Line3.GetComponent<MeshRenderer>().material = matList[matNum];
                Danger.transform.GetChild(figNum).GetComponent<MeshRenderer>().material = matList[matNum];

                Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                    new Vector3(1.4f, 1.54f, 0.422f), 1.0f * Time.deltaTime);
                Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                    new Vector3(1.4f, 0.9f, -0.567f), 1.0f * Time.deltaTime);
                Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                    new Vector3(1.4f, 1.25f, -0.07f), 1.0f * Time.deltaTime);

                Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                    Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);
                Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                    Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);
                Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                    Quaternion.Euler(0, 0, 0), 3.0f * Time.deltaTime);

                if (Line1.transform.localScale.z <= 0.2f)
                {
                    Line1.transform.localScale += upPos;
                }

                else
                {
                    Line1.transform.localScale += downPos;
                }

                if (Line2.transform.localScale.z <= 0.2f)
                {
                    Line2.transform.localScale += upPos;
                }

                else
                {
                    Line2.transform.localScale += downPos;
                }

                if (Line3.transform.localScale.z <= 0.7f)
                {
                    Line3.transform.localScale += upPos;
                }

                else
                {
                    Line3.transform.localScale += downPos;
                }

                if (Line1.transform.position == new Vector3(1.4f, 1.54f, 0.422f) &&
                    Line2.transform.position == new Vector3(1.4f, 0.9f, -0.567f) &&
                    Line3.transform.position == new Vector3(1.4f, 1.25f, -0.07f))
                {
                    col1.SetActive(true);
                    col2.SetActive(true);
                    col3.SetActive(true);
                    col4.SetActive(true);

                    col1.transform.position = new Vector3(1.4f, 1.5f, 0.22f);
                    col2.transform.position = new Vector3(1.4f, 1.5f, -0.7f);
                    col3.transform.position = new Vector3(1.4f, 0.9f, -0.36f);
                    col4.transform.position = new Vector3(1.4f, 0.9f, 0.64f);

                    isColliding = false;
                }
            }
        }

        if((figNum == 0 && collider1) || (figNum == 4 && collider1))
        {
            rand = false;
            collider1 = false;

            if (figCnt == 8)
            {
                figCnt++;
                isColliding = false;
            }

            else if(figCnt < 8)
            {
                if (!ivk)
                {
                    Invoke("ColTrue", 0.5f);
                    ivk = true;
                }
            }
        }

        if(collider1 && collider2)
        {
            rand = false;
            collider1 = collider2 = false;

            if(figCnt == 8)
            {
                figCnt++;
                isColliding = false;
            }

            else if(figCnt < 8)
            {
                if (!ivk)
                {
                    Invoke("ColTrue", 0.5f);
                    ivk = true;
                }
            }
        }

        if(figCnt >= 8 && !makingArrow)
        {
            FigureFin = true;
            Ikinema.SetActive(false);

            Line1.SetActive(true);
            Line2.SetActive(true);
            Line3.SetActive(true);

            Line4.SetActive(false);
            Line5.SetActive(false);

            col1.SetActive(false);
            col2.SetActive(false);
            col3.SetActive(false);
            col4.SetActive(false);

            Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                new Vector3(0.05f, 1.216f, 1.136f), 0.3f * Time.deltaTime);
            Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                new Vector3(0.576f, 1.374f, 1.136f), 0.3f * Time.deltaTime);
            Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                new Vector3(0.576f, 1, 1.136f), 0.3f * Time.deltaTime);

            Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                Quaternion.Euler(0, -90f, 0), 1.5f * Time.deltaTime);
            Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                Quaternion.Euler(-45f, -90f, 0), 1.5f* Time.deltaTime);
            Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                Quaternion.Euler(45f, -90f, 0), 1.5f * Time.deltaTime);

            if (Line1.transform.localScale.z > 0.4f)
            {
                Line1.transform.localScale -= scales;
            }

            else
            {
                Line1.transform.localScale = new Vector3(0.05f, 0.05f, 0.4f);
            }

            if (Line2.transform.localScale.z > 0.3f)
            {
                Line2.transform.localScale -= scales;
            }

            else
            {
                Line2.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            }

            if (Line3.transform.localScale.z > 0.3f)
            {
                Line3.transform.localScale -= scales;
            }

            else
            {
                Line3.transform.localScale = new Vector3(0.05f, 0.05f, 0.3f);
            }

            if (Line1.transform.position == new Vector3(0.05f, 1.216f, 1.136f) &&
                Line2.transform.position == new Vector3(0.576f, 1.374f, 1.136f) &&
                Line3.transform.position == new Vector3(0.576f, 1, 1.136f) &&
                Line1.transform.localScale == new Vector3(0.05f, 0.05f, 0.4f) &&
                Line2.transform.localScale == new Vector3(0.05f, 0.05f, 0.3f) &&
                Line3.transform.localScale == new Vector3(0.05f, 0.05f, 0.3f))
            {
                if(!ivk)
                {
                    Invoke("makeArrows", 2.0f);
                    ivk = true;
                }
            }
        }

        if(makingArrow && !arr)
        {
            Line1.transform.SetParent(Arrows.transform);
            Line2.transform.SetParent(Arrows.transform);
            Line3.transform.SetParent(Arrows.transform);

            Arrows.transform.position = Vector3.MoveTowards(Arrows.transform.position,
                new Vector3(-0.564f, 0.954f, 0.471f), 0.5f * Time.deltaTime);
            Arrows.transform.rotation = Quaternion.Slerp(Arrows.transform.rotation,
                Quaternion.Euler(0, 0, 45), 1.5f * Time.deltaTime);

            if(Arrows.transform.position == new Vector3(-0.564f, 0.954f, 0.471f))
            {
                arr = true;
                StartCoroutine(timeChecker());
            }
        }

        if(arr && timeFin)
        {
            Spring.SetActive(false);
            Arrows.transform.SetParent(nullPar.transform);

            Line1.transform.position = Vector3.MoveTowards(Line1.transform.position,
                new Vector3(-0.898f, 1.26f, 0.1f), 0.5f * Time.deltaTime);
            Line1.transform.rotation = Quaternion.Slerp(Line1.transform.rotation,
                Quaternion.Euler(0, -49.852f, 0), 1.0f * Time.deltaTime);
            Line2.transform.position = Vector3.MoveTowards(Line2.transform.position,
                new Vector3(-0.898f, 1.26f, 0.1f), 0.5f * Time.deltaTime);
            Line2.transform.rotation = Quaternion.Slerp(Line2.transform.rotation,
                Quaternion.Euler(0, -49.852f, 0), 1.0f * Time.deltaTime);
            Line3.transform.position = Vector3.MoveTowards(Line3.transform.position,
                new Vector3(-0.898f, 1.26f, 0.1f), 0.5f * Time.deltaTime);
            Line3.transform.rotation = Quaternion.Slerp(Line3.transform.rotation,
                Quaternion.Euler(0, -49.852f, 0), 1.0f * Time.deltaTime);
            Line1.transform.GetComponent<MeshRenderer>().material = black;
            Line2.transform.GetComponent<MeshRenderer>().material = black;
            Line3.transform.GetComponent<MeshRenderer>().material = black;

            if(Line1.transform.localScale.z <= 2f)
            {
                Line1.transform.localScale += new Vector3(0, 0, 0.01f);
            }

            else
            {
                Line1.transform.localScale = new Vector3(0.1f, 0.1f, 2f);
            }

            if (Line2.transform.localScale.z <= 2f)
            {
                Line2.transform.localScale += new Vector3(0, 0, 0.01f);
            }

            else
            {
                Line2.transform.localScale = new Vector3(0.1f, 0.1f, 2f);
            }

            if (Line3.transform.localScale.z <= 2f)
            {
                Line3.transform.localScale += new Vector3(0, 0, 0.01f);
            }

            else
            {
                Line3.transform.localScale = new Vector3(0.1f, 0.1f, 2f);
            }

            if (Line1.transform.position == new Vector3(-0.898f, 1.26f, 0.1f) &&
                Line2.transform.position == new Vector3(-0.898f, 1.26f, 0.1f) &&
                Line3.transform.position == new Vector3(-0.898f, 1.26f, 0.1f) &&
                Line1.transform.localScale.z >= 2f &&
                Line2.transform.localScale.z >= 2f &&
                Line3.transform.localScale.z >= 2f)
            {
                Invoke("Load", 2.0f);
            }
        }
    }

    IEnumerator timeChecker()
    {
        while(!timeFin)
        {
            time += 0.1f;

            if(time >= 30f)
            {
                timeFin = true;
            }

            yield return new WaitForSeconds(0.1f);
        }
    }

    void Load()
    {
        SceneManager.LoadScene("User Plane Scene");
    }

    void makeArrows()
    {
        makingArrow = true;
    }

    void ColTrue()
    {
        isColliding = true;
        SetActiveFalse();
        figCnt++;
        ivk = false;
    }

    void RandomValue()
    {
        bool fig = false;
        bool mat = false;

        while (!fig)
        {
            float num = Random.value * 1000;

            figNum = System.Convert.ToInt32(num) % 8;

            if (figureList[figNum])
            {
                continue;
            }

            else
            {
                figureList[figNum] = true;
                break;
            }
        }

        while (!mat)
        {
            float num2 = Random.value * 1000;

            matNum = System.Convert.ToInt32(num2) % 8;

            if(matListBool[matNum])
            {
                continue;
            }

            else
            {
                matListBool[matNum] = true;
                matCnt++;
                break;
            }
        }
    }

    void SetActiveFalse()
    {
        Line1.SetActive(false);
        Line2.SetActive(false);
        Line3.SetActive(false);
        Line4.SetActive(false);
        Line5.SetActive(false);

        col1.SetActive(false);
        col2.SetActive(false);
        col3.SetActive(false);
        col4.SetActive(false);
    }
}
